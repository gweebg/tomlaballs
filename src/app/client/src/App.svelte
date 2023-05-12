<script>

  import {convertFromToml} from "./lib/scripts/convert.js";
  import {shortcut} from "./lib/scripts/shortcut.js";

  import TextOutput from "./lib/TextOutput.svelte";

  let tomlValue = "";
  let jsonValue = "";

  const convert = async (data) => {

    const {result, valid, message} = await convertFromToml(data);

    if (valid) jsonValue = JSON.parse(result);
    else jsonValue = message;

  }


</script>

<main>

  <div class="header">

    <div class="logo">
       <a href="https://github.com/gweebg/tomlaballs" target="_blank">
           <h1>TOMLABALLS</h1>
           <p>Yet another TOML to JSON parser.</p>
       </a>
    </div>

  </div>


  <div class="input-grid">


      <textarea
              name="toml_value"
              id="toml" cols="70"
              rows="30"
              placeholder="Insert your TOML code here."
              bind:value={tomlValue}
              use:shortcut={{control: true, code: 'Enter', callback: () => convert(tomlValue)}}></textarea>

      <TextOutput on:convert={() => {convert(tomlValue)}} content={jsonValue}/>

  </div>

</main>

<style>

  .header {
    display: flex;
    justify-content: center;
    align-items: end;
  }

  .logo {
    border-radius: 8px;
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
