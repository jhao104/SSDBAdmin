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


if __name__ == '__main__':
    print(getPagingTabsInfo(10, 5, 5))
