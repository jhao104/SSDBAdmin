# 进一法求分页的总数
def get_paging_tabs_total(total_count, per_page_count):
    return (total_count + per_page_count - 1) / per_page_count


# 矫正分页的变量
def correct_paging_tabs_index(page_count, page_num):
    return max(min(page_num, page_count), 1)


# 获取分页信息
def get_paging_tabs_info(data_count, page_no, page_row_num=20):
    page_count = get_paging_tabs_total(int(data_count), int(page_row_num))
    page_num = correct_paging_tabs_index(page_count, int(page_no))
    return page_count, page_num


if __name__ == '__main__':
    print(get_paging_tabs_info(10, 3, 5))
