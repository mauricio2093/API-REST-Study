const axios = require('axios');

const url = 'https://xkcd.com/info.0.json';

const callData = async (url) => {
    try {
        const pos = await axios(url);
        console.log(pos.data);
    } catch(error){
        console.log(error);
    }
}

callData(url);
