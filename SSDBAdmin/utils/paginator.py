# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     paginator
   Description :   paging function
   Author :        JHao
   date：          2018/8/27
-------------------------------------------------
   Change Activity:
                   2018/8/27: paging function
-------------------------------------------------
"""
__author__ = 'JHao'


# 进一法求分页的总数
def _getPagingTabsTotal(total_count, per_page_count):
    return (total_count + per_page_count - 1) // per_page_count


# 矫正分页的变量
def _correctPagingTabsIndex(page_count, page_num):
    return max(min(page_num, page_count), 1)


# 获取分页信息
def getPagingTabsInfo(data_count, page_no, page_row_num=20):
    page_count = _getPagingTabsTotal(int(data_count), int(page_row_num))
    page_num = _correctPagingTabsIndex(page_count, int(page_no))
    return page_count, page_num


# 计算页码
def getPageNumberInfo(data_index, page_count, per_page_num):
    """
    计算数据位于的页码
    Args:
        data_index: 数据位置索引
        page_count: 总页码数
        per_page_num: 每页数量
    Returns:
        页码(int)
    """
    page_index = (int(data_index) // int(per_page_num)) + 1
    total_index = int(page_count) * int(per_page_num)
    if int(data_index) == total_index:
        return int(page_count)
    return page_index if data_index <= total_index else 1


if __name__ == '__main__':
    print(getPagingTabsInfo(20, 7, 5))
    print(getPageNumberInfo(121, 3, 10))
