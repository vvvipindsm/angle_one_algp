let { SmartAPI, WebSocketV2 } = require("smartapi-javascript");
const { CONSTANTS, MODE, ACTION, EXCHANGES } = require("smartapi-javascript/config/constant");



let web_socket = new WebSocketV2({
	jwttoken: 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlYxNTQ3NzIiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwidG9rZW4iOiJleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKbGVIQWlPakUyT1RJeU5qWTVOemtzSW1saGRDSTZNVFk1TWpFM016YzVPQ3dpYjIxdVpXMWhibUZuWlhKcFpDSTZNU3dpYzI5MWNtTmxhV1FpT2lJeklpd2ljM1ZpSWpvaVZqRTFORGMzTWlKOS5zMTE0dnFQa3l4QVg2WDZfY1J0d0VOem1UWEhqNXY1TkdnM0NGZi0zT0huWUplSHlxbWlkVjMwZ2FFTkp2dkhlSGh3X1liRUo4YTh2elpRaE1JeG9uUSIsImlhdCI6MTY5MjE3Mzg1OCwiZXhwIjoxNjkyMjYwMjU4fQ.JnvqLomK2LkWUQJfDQSSMvULnMOxdEvmjVK7ZLUrnEkkX8m81IH0hgIF8qdhYHNO06VmtW90a-7zAOtffll1BQ',
	apikey: 'Q1TIE8hH',
	clientcode: 'V154772',
	feedtype: 'eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlYxNTQ3NzIiLCJpYXQiOjE2OTIxNzM4NTgsImV4cCI6MTY5MjI2MDI1OH0.cf8eLdF7kZaPk_ON-wseXHZBYZEbV3WEjE_kvjmKCt3GRBHZcQ8KL0EQ9wkcQy0AqaGVokYLOF_7p7f5YkQkSQ',
});
//web_socket.connect()
   
web_socket.connect()
.then((res) => {
	let json_req = {
        "correlationID": "abcde12345",
        "action": ACTION.Subscribe,
        "token" : ["1333" ],
        "mode" : MODE.SnapQuote,
        "exchangeType" : EXCHANGES.nse_cm
   }
	web_socket.fetchData(json_req);
	web_socket.on('tick', receiveTick);

	function receiveTick(data) {
	 	console.log('receiveTick:::::', data);
	 }
});

