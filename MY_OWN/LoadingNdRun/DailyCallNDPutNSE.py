#!/usr/bin/env python
# coding: utf-8

# In[58]:



import requests
from bs4 import BeautifulSoup
from datetime import datetime

from selenium import webdriver


driver = webdriver.Chrome()
driver.get("https://groww.in/options/nifty")
data = driver.execute_script('''
   setTimeout(function() {
          const o_t = document.querySelectorAll("table")[0]
            op_t_tbody = o_t.querySelector('tbody')
        op_t_tbody_trs = op_t_tbody.querySelectorAll('tr')
        let result = []
        op_t_tbody_trs.forEach((data,x)=>{
        let temp = {}
       // console.log(x)
        if( x < 53){
        try{
        console.log(x)
        //console.log(op_t_tbody_trs[x])
        tr = op_t_tbody_trs[x]
        tds = tr.querySelectorAll('td')
        //console.log(tds)
        strike = tds[3]

        strike_div = strike.querySelector('div')
        strike_inner_div = strike_div.querySelector('div')
        //console.log(strike_inner_div)
        temp["strike"] = strike_inner_div.innerText
        //console.log(temp)
        const current_date =new Date().toISOString()
         //call price
        call_pr = tds[2]
        call_a = call_pr.querySelector('a')
        temp["call_price"] = call_a.innerText
        temp["date"] = current_date

        //put price 
        put_pr = tds[4]
        put_a = put_pr.querySelector('a')
        temp["put_price"] = put_a.innerText
        //oi
        divs = tds[1].querySelectorAll("div")
        innerDiv = divs[1].querySelector("div")
        innerDiv1 = innerDiv.querySelectorAll("div")

        temp["oi"] = innerDiv1[0].innerText
        temp["oi_p"] = innerDiv1[1].innerText
        //oi call
        divs = tds[5].querySelectorAll("div")
        innerDiv = divs[1].querySelector("div")
        innerDiv1 = innerDiv.querySelectorAll("div")

        temp["oi_call"] = innerDiv1[0].innerText
        temp["oi_call_p"] = innerDiv1[1].innerText
        
        //console.log(temp)
        result.push(temp)
        }catch(err){
            console.log("err")
        }

        }
    })
    document.title = JSON.stringify(result)
    window.open("https://smarttradersclub.in/api_214124524/oi_runner.php?data="+JSON.stringify(result),'_blank');

    return result
  }, 2000);
  return "result"
''')

#driver.quit()
print("Title:", data)


