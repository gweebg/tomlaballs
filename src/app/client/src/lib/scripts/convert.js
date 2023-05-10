
async function convertFromToml(tomlData) {

  const response = await fetch('http://localhost:8000/convert', {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json'
      },

      body: JSON.stringify(
          { data: tomlData, convert_lang: "json" }
      )

    });

  const { result, valid, message } = await response.json();
  return { result, valid, message };

}

export { convertFromToml };
