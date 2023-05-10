<script>

  import {convertFromToml} from "./lib/scripts/convert.js";
  import {shortcut} from "./lib/scripts/shortcut.js";

  let tomlValue = "";
  let jsonValue = "";

  const convert = async (data) => {

    console.log("At 'convert'!");

    const {result, valid, message} = await convertFromToml(data);

    if (valid) {
      jsonValue = result;
    } else jsonValue = message;

  }

</script>

<main>

  <h1>TOMLABALLS</h1>
  <p>Yet another TOML to JSON parser.</p>

  <div class="input-grid">

    <form>

      <textarea
              name="toml_value"
              id="toml" cols="70"
              rows="30"
              placeholder="Insert your TOML code here."
              bind:value={tomlValue}
              use:shortcut={{control: true, code: 'Enter', callback: () => convert(tomlValue)}}></textarea>

      <textarea bind:value={jsonValue} name="json_value" id="json" cols="70" rows="30" readonly placeholder="The JSON output shows up here! Press CTRL + ENTER to convert!"></textarea>

    </form>


  </div>

  <p class="footer">Check out the project at <a href="https://github.com/gweebg/tomlaballs">tomlaballs</a></p>

</main>

<style>

  .input-grid {
    display: flex;
    flex-direction: row;
  }

  .input-grid-item {
    margin-right: 20px;
    height: 700px;
    width: 700px;
    background: white;
    border-radius: 7px;
  }

  textarea {
    resize: none;
    font-size: 18px;
    padding: 10px;
  }

  p {
    margin-top: 0;
    margin-bottom: 2rem;
    line-height: 1.1;
  }

  .footer {
    margin-bottom: 0;
    line-height: 1.1;
  }

</style>
