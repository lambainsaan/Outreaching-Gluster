#include <stdio.h>
#include <glusterfs/api/glfs.h>
#include <glusterfs/api/glfs-handles.h>
#include <errno.h>
#include <string.h>
#include <time.h>

glfs_t *fs = NULL;

int main(int argc, char const *argv[])
{
    int ret = 0;
    unsigned long currentTime = time(NULL);
    char *serverName = "server1";
    char *volName = "gv1";
    char filename[25];
    char fileContent[25];
    
    sprintf(filename, "file %lu.txt", currentTime);
    sprintf(fileContent, "File since %lu", currentTime);
    
    glfs_fd_t *fd = NULL;
    fs = glfs_new(volName);

    ret = glfs_set_volfile_server(fs, "tcp", serverName, 24007);
    if (ret) {
        fprintf(stderr, "Could not Specify the list of addresses for management server: %s", strerror(errno));
        return -1;
    }

    ret = glfs_init(fs);
    if (ret) {
        fprintf(stderr, "Could not initialize the 'virtual mount': %s", strerror(errno));
        return -1;
    }


    glfs_creat(fs, filename, O_CREAT, 0644);

    fd = glfs_open(fs, filename, O_RDWR);

    glfs_write(fd, fileContent, 21, 0);
    glfs_close(fd);

    return ret;
}

