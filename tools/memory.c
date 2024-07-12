#define _GNU_SOURCE
#include <sys/uio.h>

ssize_t read_process_memory(pid_t pid, void *local_addr, void *remote_addr, size_t len, size_t scatter)
{
    struct iovec local[scatter];
    struct iovec remote[scatter];

    local[0].iov_base = local_addr;
    local[0].iov_len = len;
    remote[0].iov_base = remote_addr;
    remote[0].iov_len = len;

    return process_vm_readv(pid, local, scatter, remote, scatter, 0);
}
