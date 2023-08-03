const tbl = document.querySelectorAll('table')[0].querySelector('tbody').querySelectorAll('tr')
let result = []
function getMonth(data){
    const year = data.split(" ")[1]
    const monthText = data.split(" ")[0]
    switch(monthText){
              case "Jan":
            return year+"-"+"01-01"
        case "Feb":
            return year+"-"+"02-01"
        case "Mar":
            return year+"-"+"03-01"
          case "Apr":
            return year+"-"+"04-01"
        case "May":
            return year+"-"+"05-01"
              case "Jun":
            return year+"-"+"06-01"
        case "Jul":
            return year+"-"+"07-01"
        case "Aug":
            return year+"-"+"08-01"
        case "Sep":
            return year+"-"+"09-01"
        case "Oct":
            return year+"-"+"10-01"
        case "Nov":
            return year+"-"+"11-01"
         case "Dec":
            return year+"-"+"12-01"
    }
}
for(let i =0;i< tbl.length;i++){
    let temp = {}
    const tItem = tbl[i].querySelectorAll('td')
    temp.date = getMonth(tItem[0].querySelector("span").innerText)
    temp.Close = tItem[1].querySelector("span").innerText
    result.push(temp)

    
}
console.log(result)