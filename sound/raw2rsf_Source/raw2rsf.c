/* See more details at https://tiebing.blogspot.com/2019/09/lego-ev3-sound-file-rsf-format.html */

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(int argc, char** argv) {
    int i;
    int count;
    char buf[1024];
    if (argc != 2) {
        printf("\n Usage: %s <input-raw-audio-file>\n", argv[0]);
        return -1;
    }
    char* infile = argv[1];
    int fd = open(infile, O_RDONLY);
    if (fd < 0) {
        perror("open error\n");
        return -1;
    }
    off_t fsize = lseek(fd, 0, SEEK_END);
    if (fsize < 0) {
        perror("lseek error\n");
        return -1;
    }

    if (fsize > 65535) {
        fprintf(stderr, "Error: input file large than 65535 bytes\n");
        return -1;
    }
    lseek(fd, 0, SEEK_SET);

    buf[0] = 0x01;
    buf[1] = 0x00;
    buf[2] = fsize / 256;
    buf[3] = fsize % 256;
    buf[4] = 0x1f;
    buf[5] = 0x40;
    buf[6] = 0x00;
    buf[7] = 0x00;
    write(1, buf, 8);

    while ((count = read(fd, buf, sizeof(buf))) > 0) {
        write(1, buf, count);
    }

    close(fd);

    return 0;
}