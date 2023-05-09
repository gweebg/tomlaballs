<script>

  import {convertFromToml} from "./lib/scripts/convert.js";
  import {shortcut} from "./lib/scripts/shortcut.js";

  let tomlValue = "";
  let jsonValue = "";



</script>

<main>

  <h1>Yet Another TOML Parser</h1>

  <div class="input-grid">

    <form>

      <textarea
              name="toml_value"
              id="toml" cols="70"
              rows="30"
              placeholder="Insert your TOML code here."
              bind:value={tomlValue}
              use:shortcut={{control: true, code: 'Enter', callback: () => jsonValue = tomlValue}}></textarea>

      <textarea bind:value={jsonValue} name="json_value" id="json" cols="70" rows="30" readonly placeholder="The JSON output shows up here! Press CTRL + ENTER to convert!"></textarea>

    </form>

  </div>

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
  }

</style>
