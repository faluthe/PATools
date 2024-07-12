from dataclasses import dataclass

def get_region_info(region_line_split):
        start, end = region_line_split[0].split("-")
        perms = region_line_split[1]
        return int(start, 16), int(end, 16), perms


def is_standard_lib(pathname):
    std_libs = ["/lib/", "/lib64/", "/usr/lib/", "/usr/lib64/", "[vdso]", "[vsyscall]", "[vvar]"]
    return any(lib in pathname for lib in std_libs)


@dataclass
class Region:
    start: int
    end: int
    perms: str
    pathname: str


@dataclass
class MemoryMap:
    stack: Region
    heap: Region
    regions: list[Region]


def get_memory_map(pid):
    regions = []
    with open(f"/proc/{pid}/maps", "r") as map_file:
        for line in map_file:
            split_line = line.split(" ")
            pathname = split_line[-1].strip()

            if is_standard_lib(pathname):
                continue
            elif pathname == "[stack]":
                start, end, perms = get_region_info(split_line)
                stack = Region(start, end, perms, pathname)
            elif pathname == "[heap]":
                start, end, perms = get_region_info(split_line)
                heap = Region(start, end, perms, pathname)
            else:
                start, end, perms = get_region_info(split_line)
                if "s" not in perms and ("r" in perms or "x" in perms):
                    regions.append(Region(start, end, perms, pathname))

    return MemoryMap(stack, heap, regions)