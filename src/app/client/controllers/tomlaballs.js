const axios = require('axios');

// Convert the TOML data to the inserted language.
module.exports.convert = data => {

    return axios.post("http://localhost:8000/convert", data)
        .then(response => {return response.data})
        .catch(error => {return error});

}