import os
import random
import sys
import shutil

from shapenet_loader import ShapeNetLoader
from shapenet_loader import ScoredResult

MAX_PER_TERM = 4
MAX_ITEMS = 3000

"""
This script builds a subset of ShapeNetSen screenshot data from the full set.
It builds a set from the top items per each term.
Then it selects a maximum number of items from that set.
Then it uses 1 out of 3 of each of the 12 images for each item.

Here is an example of the difference in size:
$ ls -l shapenet/models-screenshots.zip 
-rw-rw-r-- 1 ranton ranton 12166065866 Jun 10  2015 shapenet/models-screenshots.zip
$ ls -l  small_shapenet.zip 
-rw-rw-r-- 1 ranton ranton 846039768 May 26 19:22 small_shapenet.zip


"""

def main():
    if len(sys.argv) < 3:
        print("Please pass <srcdir> and <dstdir>")
        return 

    src_datadir = sys.argv[1]
    dst_datadir = sys.argv[2]

    
    loader = ShapeNetLoader(src_datadir)
    loader.load()

    print("original size:", loader.record_count())

    # get subset of metadata

    # drop any row from the matching list of a term past the top k highest scored.
    # this doesn't reduce things much beyond 4

    keep_ids_set = set()   
    for term in loader.all_terms():
        sr = loader.get_scored_results_for_term(term)
        full_ids = [x.full_id for x in sr]
        #print("{} -> {}".format(term, ','.join(full_ids)))
        k = min(MAX_PER_TERM, len(full_ids))
        keep_ids = full_ids[:k]
        keep_ids_set.update(keep_ids)


    # drop what's left over a max amount.
    # use a fixed seed so it's repeatable which set we get
    random.seed(6512714)
    shuffled_ids = list(keep_ids_set)
    random.shuffle(shuffled_ids)

    keep_ids_set = set(shuffled_ids[:MAX_ITEMS])


    print("keep ids set count:", len(keep_ids_set))
    
    # For every id still in the list

    # Write updated metadata that only has rows which are in the set we built.
    df = loader.metadata_df

    drop_idx_set = set()
    for row in df.itertuples():
        if row.fullId not in keep_ids_set:
            drop_idx_set.add(row.Index)

    df.drop(list(drop_idx_set), inplace=True)
    
    print("remaining size:", loader.record_count())


    if not os.path.exists(dst_datadir):
        os.makedirs(dst_datadir)
    csv_path = os.path.join(dst_datadir, "metadata.csv")
    df.to_csv(path_or_buf=csv_path, index=False)

    
    # copy the desired images for each row still in dataset.
    n_min = 999999
    n_max = -1
    total = 0
    cnt = 0
    for row in df.itertuples():
        full_id = row.fullId
        image_paths = loader.get_image_paths_for_id(full_id)
        image_paths = sorted(image_paths)
        n = len(image_paths)
        cnt = cnt + 1
        total = total + n
        if n < n_min:
            n_min = n
        if n > n_max:
            n_max = n
        # all of the items have 14 images
        # they are different views in shapenet
        # the README for shapenet says:
        # - models-screenshots.zip : Pre-rendered screenshots of each model from 6 canonical orientations 
        # (front, back, left, right, bottom, top), and another 6 "turn table" positions around the model
        # It is not clear which view are better for which image, so let's just take mod 3 == 2
        id_dir_name = loader.get_id_dir_name(full_id)
        dst_dir_path = os.path.join(dst_datadir, "screenshots", id_dir_name)
        if not os.path.exists(dst_dir_path):
            os.makedirs(dst_dir_path)

        selected = []
        for c, src_path in enumerate(image_paths):
            if c % 3 == 0:
                bn = os.path.basename(src_path)
                dst_path = os.path.join(dst_dir_path, bn)
                print("copy from {} -> {}".format(src_path, dst_path))
                try:
                    shutil.copy(src_path, dst_path)
                except IOError as e:
                    print("Error copying file from {} to {}: {}".format(src_path, dst_path, e))

    #print("min={} max={} avg={}".format(n_min, n_max, float(total)/max(cnt,1)))
    
    # copy readme and other relevant information.
    for p in ["README.txt","info.txt"]:
        src_path = os.path.join(src_datadir,  p)
        dst_path = os.path.join(dst_datadir,  p)
        try:
            shutil.copy(src_path, dst_path)
        except IOError as e:
            print("Error copying file from {} to {}: {}".format(src_path, dst_path, e))
    

if __name__ == "__main__":
    main()
