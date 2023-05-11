<script>

  import {convertFromToml} from "./lib/scripts/convert.js";
  import {shortcut} from "./lib/scripts/shortcut.js";

  import {Highlight, LineNumbers} from "svelte-highlight";
  import {json} from "svelte-highlight/languages";
  import {atelierPlateau} from "svelte-highlight/styles";

  let tomlValue = "";
  let jsonValue = "";

  const convert = async (data) => {

    const {result, valid, message} = await convertFromToml(data);

    if (valid) {
      let resultJson = JSON.parse(result);
      document.getElementById('json').innerHTML = JSON.stringify(resultJson, undefined, 4);
    } else {
      document.getElementById('json').innerHTML = message;
    }

  }

</script>

<main>

  <div class="header">

    <div class="logo">
      <h1>TOMLABALLS</h1>
      <p>Yet another TOML to JSON parser.</p>
    </div>


    <div class="controls">

      <button>Convert</button>
      <button>Settings</button>
      <button>Copy to Clipboard</button>

    </div>

  </div>


  <div class="input-grid">

    <form>

      <textarea
              name="toml_value"
              id="toml" cols="70"
              rows="30"
              placeholder="Insert your TOML code here."
              bind:value={tomlValue}
              use:shortcut={{control: true, code: 'Enter', callback: () => convert(tomlValue)}}></textarea>

      <textarea name="json_value" id="json" cols="70" rows="30" readonly placeholder="The JSON output shows up here! Press CTRL + ENTER to convert!"></textarea>

    </form>
  </div>

  <p class="footer">Check out the project at <a href="https://github.com/gweebg/tomlaballs">tomlaballs</a></p>

</main>

<style>

  .header {
    display: flex;
    justify-content: space-between;
    align-items: end;
  }

  .logo {
    background: #1a1a1a;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
  }

  .controls {
    margin-bottom: 20px;
  }

  .input-grid {
    display: flex;
    flex-direction: row;
  }

  textarea {
    resize: none;
    font-size: 18px;
    padding: 10px;
    transition: border-color 0.25s;
  }

  textarea:hover {
    border-color: #646cff;
  }

  textarea:focus {
    outline: none #646cff;
  }

  p {
    margin: 0;
    line-height: 1.1;
  }

  .footer {
    margin-bottom: 0;
    line-height: 1.1;
  }

</style>
