set -e

echo "=== gen =="
test -f file0_1k.txt   || seq      1001 | shuf > file0_1k.txt
test -f file1_100k.txt || seq    100001 | shuf > file1_100k.txt
test -f file2_10M.txt  || seq  10000001 | shuf > file2_10M.txt
test -f file3_100M.txt || seq 100000001 | shuf > file3_100M.txt

echo "=== gcc =="
gcc -O3 -g  correction.c -o correction

for f in file*.txt; do
	echo "=== test: $f ==="
	for i in `seq 3`; do
		time ./correction "$f"
	done
done
