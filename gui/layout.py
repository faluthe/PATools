import dearpygui.dearpygui as dpg
from gui.callbacks import attach_cb, memory_view_cb, memory_mappings_cb, filter_cb, save_address_cb, resize_cb
from tools.proc_list import get_proc_list


# TBD: Delete this
def print_me(sender):
    print(f"Menu Item: {sender}")


def init_global_state():
    with dpg.value_registry():
        dpg.add_int_value(default_value=-1, tag="attached_proc")


def init_primary_window():
    
    def init_menu_bar():
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Save", callback=print_me)
                dpg.add_menu_item(label="Save As", callback=print_me)

                with dpg.menu(label="Attach"):
                    dpg.add_input_text(label="Filter", callback=filter_cb)
                    proc_list = get_proc_list()
                    with dpg.group(tag="attach_proc_group"):
                        for proc_name, pid in proc_list:
                            dpg.add_menu_item(label=f"{proc_name}({pid})", callback=attach_cb, user_data=(proc_name, pid))


            dpg.add_menu_item(label="Help", callback=print_me)


    def init_search_table():
        with dpg.group(horizontal=True):
            with dpg.child_window(tag="search_table", height=300):
                with dpg.table(row_background=True, clipper=True) as selectablerows:
                    dpg.add_table_column(label="Address")
                    dpg.add_table_column(label="Value")

                    for value in range(30):
                        with dpg.table_row():
                            dpg.add_selectable(label=f"0x{value:08x}", span_columns=True, callback=save_address_cb, user_data=(f"0x{value:08x}", value, "int"), height=20)
                            dpg.add_text(f"{value}")

                dpg.bind_item_theme(selectablerows, "table_theme")

            with dpg.group(horizontal=False):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="First Scan", callback=print_me, height=30)
                    dpg.add_button(label="Next Scan", callback=print_me, height=30)

                dpg.add_input_text(tag="search_val", height=30)


    def init_saved_table():
        with dpg.child_window():
            with dpg.table(row_background=True, clipper=True, tag="saved_addresses"):
                dpg.add_table_column(label="Address")
                dpg.add_table_column(label="Value")
                dpg.add_table_column(label="Type")

            dpg.bind_item_theme("saved_addresses", "table_theme")


    with dpg.window(tag="Primary Window"):
        init_menu_bar()

        dpg.add_text("No Process Selected.", tag="attached_proc_label")

        dpg.add_progress_bar(default_value=0.0, tag="search_progress", width=dpg.get_viewport_width() - 16, height=30)

        init_search_table()

        with dpg.table(header_row=False):
            for _ in range(3):
                dpg.add_table_column()
            with dpg.table_row():
                dpg.add_button(label="Memory View", callback=memory_view_cb, tag="memory_view_button", width=(dpg.get_viewport_width() // 3) - 12, height=30)
                dpg.add_text()
                dpg.add_button(label="Add Address Manually", callback=print_me, tag="add_address_button", width=(dpg.get_viewport_width() // 3) - 12, height=30)

        init_saved_table()


def init_memory_view_window():
    with dpg.window(label="Memory View", tag="memory_view_window", modal=False, width=600, height=600, show=False, no_collapse=True):
        with dpg.menu_bar():
            with dpg.menu(label="View"):
                dpg.add_menu_item(label="Memory Mappings", callback=memory_mappings_cb)


def init_memory_mappings_window():
    with dpg.window(label="Memory Mappings", tag="memory_mappings_window", modal=False, width=600, height=300, show=False, no_collapse=True):
        with dpg.table(row_background=True, clipper=True, tag="memory_mappings_table"):
            dpg.add_table_column(label="Pathname")
            dpg.add_table_column(label="Start")
            dpg.add_table_column(label="End")
            dpg.add_table_column(label="Perms")

        dpg.bind_item_theme("memory_mappings_table", "table_theme")


def init_error_windows():
    
    def init_unattached_error():
        with dpg.window(label="Error", tag="error_window", modal=True, width=200, show=False, no_resize=True):
            dpg.add_text("No Process Attached.")

    init_unattached_error()


def init_layout():
    dpg.create_context()
    dpg.create_viewport(title="Pat's Tool")

    # Disable changing color on select
    with dpg.theme(tag="table_theme"):
        with dpg.theme_component(dpg.mvTable):
            dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0))

    init_global_state()
    init_error_windows()
    init_memory_mappings_window()
    init_memory_view_window()
    init_primary_window()

    dpg.set_viewport_resize_callback(resize_cb)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()