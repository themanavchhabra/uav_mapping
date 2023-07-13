# python3 receiver_image_text.py
# python3 copying.py

file_list=("receiver_image_text.py" "copying.py")

for py_file in "${file_list[@]}"
do
    python3 ${py_file}
done

pto_gen -o map.pto -f 42 data/images/*.png
hugin_executor -a map.pto
hugin_executor -s --prefix=stitched_map map.pto
xdg-open stitched_map.tif
