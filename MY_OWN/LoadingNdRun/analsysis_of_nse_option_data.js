const tbl = document.getElementById("optionChainTable-indices");
const t_body = document.querySelector("tbody");
const trs = document.querySelectorAll("tr");
let result = [];

trs.forEach(function(tr,index){
    let temp = {};
    if(index > 2) {
          const tds = tr.querySelectorAll("td");
          temp.call_oi = parseFloat(tds[1].innerText.replace("-","0").replace(",",""));
          temp.call_vol = parseFloat(tds[3].innerText.replace("-","0").replace(",",""));
           temp.call_bid = parseFloat(tds[8].innerText.replace("-","0").replace(",",""));
          temp.call_ask = parseFloat(tds[9].innerText.replace("-","0").replace(",",""));
         temp.strike = parseFloat(tds[11].innerText.replace("-","0").replace(",",""));
         temp.put_oi = parseFloat(tds[21].innerText.replace("-","0").replace(",",""));
          temp.put_vol = parseFloat(tds[19].innerText.replace("-","0").replace(",",""));
           temp.put_bid = parseFloat(tds[13].innerText.replace("-","0").replace(",",""));
          temp.put_ask = parseFloat(tds[14].innerText.replace("-","0").replace(",",""));

          result.push(temp);
    };
});
let currentPrice = document.getElementById("equity_underlyingVal").innerText;
currentPrice = currentPrice.split(" ").slice(-1,)[0];
currentPrice = parseFloat(currentPrice.replace(",",""));

const cut_off = currentPrice*.015;

console.log(cut_off);

let fitler_with_strike_price = result.filter(item => (item.strike > currentPrice -cut_off ) && (item.strike < currentPrice + currentPrice ));
fitler_with_strike_price = fitler_with_strike_price.map(item=> {
    return {
        ...item,
        bigger_order_dir : (item.call_oi > item.put_oi)?"call":"put",
        bigger_oi :  Math.max(item.call_oi,item.put_oi)
    };
});


fitler_with_strike_price = fitler_with_strike_price.sort(function(a,b){ 

    if(a.bigger_oi > b.bigger_oi) return -1;
});

const call_side_data = fitler_with_strike_price.filter(item=>item.bigger_order_dir == "call").slice(0,4);
const put_side_data = fitler_with_strike_price.filter(item=>item.bigger_order_dir == "put").slice(0,4);

console.log("Buy Support Area",call_side_data.map(item=>item.strike));
console.log("Sell Support Area",put_side_data.map(item=>item.strike));


