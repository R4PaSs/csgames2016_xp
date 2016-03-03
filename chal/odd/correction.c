#include <sys/stat.h>
#include <sys/mman.h> 
#include <fcntl.h>
#include <stdio.h>

int main(int argc, char **argv) {
	if (argc < 2) { printf("Need a file.\n"); return 1; }
	char *path = argv[1];
	int fd = open(path, O_RDONLY);
	if (fd == -1) { perror(path); return 1; }
	 
	int status;
	struct stat s;
	status = fstat(fd, & s);
	if (status == -1) { perror(path); return 1; }
	size_t size = s.st_size;
	//printf("%s: %ld\n", path, size);
	char *mapped = mmap(NULL, size, PROT_READ, MAP_PRIVATE, fd, 0);
	if (mapped == MAP_FAILED) { perror(path); return 1; }

	int cpt = 0;
	int last_is_odd = 0;
	size_t i;
	for (i = 0; i < size; i++) {
		char c = mapped[i];

		if (c == '\n') {
			cpt += last_is_odd;
			last_is_odd = 0;
		} else if (c >= '0' && c <= '9') {
			last_is_odd = c & 0x01;
		} else {
			printf("bad char `%c` (%x), at offset %ld.\n", c, (int)c, i);
			last_is_odd = 0;
		}
	}
	printf("%d\n", cpt);
	return 0;
}
