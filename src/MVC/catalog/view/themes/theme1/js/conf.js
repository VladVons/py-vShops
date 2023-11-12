"use strict"

// user's configuration
export const
  conf = {
    url : {
      local     : '/api/?route=system/lang&path=common/home&key=js&lang=ua',
      order_id  : '/api/?route=checkout/confirm&method=ApiOrder',
      search    : '/?route=product/search&search=',
      menu      : '/api/?route=product/category&method=ApiNav',
      history   : '/?route=checkout/history',
      category  : '/?route=product/category',
      confirm   : '/?route=checkout/confirm'
    },
    cart : {
      head: ['code','pid','name','img','url','qty','price'],
      data: [],
    }
  }
