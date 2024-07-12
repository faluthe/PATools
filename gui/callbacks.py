from tools.memory_map import get_memory_map
from tools.read_memory import read_memory
from tools.proc_list import get_proc_list
import dearpygui.dearpygui as dpg


def attach_cb(s, a, user_data):
    proc_name, pid = user_data
    dpg.set_value("attached_proc", pid)
    dpg.set_value("attached_proc_label", f"Selected Process {proc_name}({pid}), Not Tracing.")


def memory_view_cb(sender):
    if dpg.get_value("attached_proc") == -1:
        dpg.show_item("error_window")
        dpg.set_item_pos("error_window", (dpg.get_viewport_width() // 2 - 100, dpg.get_viewport_height() // 2 - 50))
    else:
        dpg.show_item("memory_view_window")
        dpg.set_item_pos("memory_view_window", (dpg.get_viewport_width() // 2 - 300, dpg.get_viewport_height() // 2 - 300))

        dpg.delete_item("memory_view_window", children_only=True)

        with dpg.menu_bar(parent="memory_view_window"):
            with dpg.menu(label="View"):
                dpg.add_menu_item(label="Memory Mappings", callback=memory_mappings_cb)

        with dpg.table(row_background=True, clipper=True, parent="memory_view_window"):
            pid = dpg.get_value("attached_proc")
            memory_map = get_memory_map(pid)
            
            dpg.add_table_column(label="Address", width_stretch=True)
            for i in range(8):
                dpg.add_table_column(width_fixed=True, init_width_or_weight=40)

            start = memory_map.heap.start
            end = memory_map.heap.end
            mem_bytes = read_memory(pid, start, end - start)

            for i in range(0, len(mem_bytes), 8):
                with dpg.table_row():
                    dpg.add_text(f"0x{start + i:08x}")
                    for j in range(8):
                        dpg.add_text(f"{mem_bytes[i + j]:02x}")


def memory_mappings_cb(sender):
    if dpg.get_value("attached_proc") == -1:
        dpg.show_item("error_window")
        dpg.set_item_pos("error_window", (dpg.get_viewport_width() // 2 - 100, dpg.get_viewport_height() // 2 - 50))
    else:
        dpg.show_item("memory_mappings_window")
        dpg.set_item_pos("memory_mappings_window", (dpg.get_viewport_width() // 2 - 300, dpg.get_viewport_height() // 2 - 150))
        
        dpg.delete_item("memory_mappings_table", children_only=True)
        
        dpg.add_table_column(label="Pathname", parent="memory_mappings_table", width_stretch=True)
        dpg.add_table_column(label="Start", parent="memory_mappings_table", width_fixed=True)
        dpg.add_table_column(label="End", parent="memory_mappings_table", width_fixed=True)
        dpg.add_table_column(label="Permissions", parent="memory_mappings_table", width_fixed=True)
        
        memory_map = get_memory_map(dpg.get_value("attached_proc"))

        with dpg.table_row(parent="memory_mappings_table"):
            dpg.add_text(memory_map.stack.pathname)
            dpg.add_text(f"0x{memory_map.stack.start:08x}")
            dpg.add_text(f"0x{memory_map.stack.end:08x}")
            dpg.add_text(memory_map.stack.perms)

        with dpg.table_row(parent="memory_mappings_table"):
            dpg.add_text(memory_map.heap.pathname)
            dpg.add_text(f"0x{memory_map.heap.start:08x}")
            dpg.add_text(f"0x{memory_map.heap.end:08x}")
            dpg.add_text(memory_map.heap.perms)

        for region in memory_map.regions:
            with dpg.table_row(parent="memory_mappings_table"):
                dpg.add_text(region.pathname)
                dpg.add_text(f"0x{region.start:08x}")
                dpg.add_text(f"0x{region.end:08x}")
                dpg.add_text(region.perms)


def filter_cb(sender):
    filter_text = dpg.get_value(sender)
    dpg.delete_item("attach_proc_group", children_only=True)

    proc_list = get_proc_list(filter_text)
    for proc_name, pid in proc_list:
        with dpg.group(parent="attach_proc_group"):
            dpg.add_menu_item(label=f"{proc_name}({pid})", callback=attach_cb, user_data=(proc_name, pid))


def save_address_cb(sender, app_data, user_data):
    address, value, data_type = user_data
    with dpg.table_row(parent="saved_addresses"):
        dpg.add_selectable(label=address, span_columns=True, callback=lambda: print("clicked"), height=20)
        dpg.add_text(value)
        dpg.add_text(data_type)


def resize_cb():
    dpg.set_item_width("search_table", (dpg.get_viewport_width() // 2) - 12)
    dpg.set_item_width("search_val", (dpg.get_viewport_width() // 2) - 12)
    dpg.set_item_width("add_address_button", (dpg.get_viewport_width() // 3) - 12)
    dpg.set_item_width("memory_view_button", (dpg.get_viewport_width() // 3) - 12)
    dpg.set_item_width("search_progress", dpg.get_viewport_width() - 16)
