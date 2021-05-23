import pandas as pd
import os
import sys
from collections import defaultdict
from collections import namedtuple

ScoredResult = namedtuple('ScoredResult', 'index, full_id, score')


class ShapeNetLoader:
    """This class is responsible for loading samples from ShapeNet dataset and other related functionality."""

    # These are the column names in metadata.csv
    # ['fullId', 'category', 'wnsynset', 'wnlemmas', 'up', 'front', 'unit', 'aligned.dims', 'isContainerLike',
    # 'surfaceVolume', 'solidVolume', 'supportSurfaceArea', 'weight', 'staticFrictionForce', 'name', 'tags']

    # NOTE: There are many rows where the category field is blank
    # NOTE: There are rows where the name field is '*'
    # NOTE: There are some weird category field values that start with underscores, like _StanfordSceneDBModels

    def __init__(self, shapenet_datadir):
        self.shapenet_datadir = shapenet_datadir
        self.metadata_df = None
        self.index = defaultdict(set)

    def load(self):
        """Load the metadata for the shapenet dataset, and build the index dict."""
        self.metadata_df = self.read_metadata()
        self.build_indexing_dict()

    def record_count(self):
        return self.metadata_df.shape[0]

    def read_metadata(self):
        metadata_df = pd.read_csv(os.path.join(self.shapenet_datadir, "metadata.csv"))
        return metadata_df

    def all_categories(self):
        categories = self.metadata_df.category.unique()
        return categories

    # We want to be able to efficiently find rows in the dataframe
    # where individual words or phrases match the noun we are looking for
    # I think the dataset metadata is small enough we can just process it into a dict that maps
    # from phrase to a set of rows that match.
    def build_indexing_dict(self):
        """Build dictionary keyed by term to set of dataframe index values for each entry."""
        for row in self.metadata_df.itertuples():
            # The category, wnlemmas, tags, and name fields all have string values
            terms = set()
            fields = [row.category, row.wnlemmas, row.tags, row.name]
            for f in fields:
                if f and isinstance(f,str):
                    parts = f.split(',')
                    for p in parts:
                        terms.add(p.lower().strip())
            for t in terms:
                # skip '*' values, not sure what these are intended to convey.
                if t == '*':
                    continue
                idx = row.Index
                self.index[t].add(idx)

    def get_rows_for_term(self, term):
        """Returns tuples of (index, row) that match term."""
        indices = self.index[term.lower().strip()]
        for idx in indices:
            row = self.metadata_df.iloc[idx]
            yield (idx, row)

    @staticmethod
    def score_row_for_term(row, term):
        """Return score for term for row based on which fields are full or partial matches."""

        fields = [row.category, row.wnlemmas, row.tags, row.name]
        match_points = [25, 5, 10, 100]
        contain_points = [10, 5, 10, 20]

        lt = term.lower()
        score = 0.0

        for z in zip(fields, match_points, contain_points):
            f, mp, cp = z
            if f and isinstance(f, str):
                f = f.lower().strip()
                if f == lt:
                    score = score + mp
                else:
                    parts = f.split(',')
                    if lt in parts:
                        score = score + cp
        return score

    def get_scored_results_for_term(self, term):
        """Get scored results, sorted by score for term."""

        # For a search term/noun score the results based on which fields the term occurs in and return sorted result.
        rows = self.get_rows_for_term(term)
        # each result is ScoredResult named tuple.
        results = []
        for (idx, row) in rows:
            score = ShapeNetLoader.score_row_for_term(row, term)
            results.append(ScoredResult(index=idx, full_id=row.fullId, score=score))
        # sort first on secondary key so order is deterministic for things with tied score.
        s = sorted(results, reverse=True, key=lambda sr: sr.full_id)
        # sort again on primary key
        return sorted(results, reverse=True, key=lambda sr: sr.score)

    def get_dir_path_for_id(self, full_id):
        """Return the directory of screenshots for a row in the dataset."""
        parts = full_id.split('.')
        if len(parts) < 2:
            # TODO: print warning about weird id
            return []
        id_dir_name = parts[1]
        return os.path.join(self.shapenet_datadir, "screenshots", id_dir_name)

    def get_image_paths_for_id(self, full_id):
        """Return the list of image paths for a row in the dataset."""
        dir_path = self.get_dir_path_for_id(full_id)
        return list(os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.png'))


def main():
    # This is a test main for playing around with the dataset."

    # TODO: we should probably build a smaller subset of shapenetsem dataset to work with out of the maximum one.

    # TODO: We need to pick an image for a term out of scored resutls.
    datadir = "shapenet"
    if len(sys.argv) > 1:
        datadir = sys.argv[1]

    loader = ShapeNetLoader(datadir)
    loader.load()
    columns = loader.metadata_df.columns.values.tolist()
    print(columns)
    print(loader.metadata_df.head())

    categories = [c for c in loader.all_categories().tolist() if isinstance(c,str)]

    other = [c for c in loader.all_categories().tolist() if not isinstance(c,str)]

    sorted_cat = sorted(categories)
    print(sorted_cat)

    print("--other--\n", other)

    top_level = set()
    for c in categories:
        parts = c.split(',')
        top_level.add(parts[0])
    print("--top_level--\n","\n".join(sorted(list(top_level))))
    print("top level count", len(top_level))

    weird = [c for c in top_level if c.startswith('_')]
    print("weird: ",weird)


    print("--Chairs--")
    chairs = loader.get_rows_for_term('chair')
    for c in chairs:
        print(c)

    scored_chairs = loader.get_scored_results_for_term('chair')
    print("sorted count", len(scored_chairs))
    print("highest score results")
    for r in scored_chairs[:5]:
        print(r)
        for p in loader.get_image_paths_for_id(r.full_id):
            print(" *", p)




if __name__ == "__main__":
    main()