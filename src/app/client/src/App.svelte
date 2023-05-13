<script>

  import {convertFromToml} from "./lib/scripts/convert.js";

  import TextOutput from "./lib/components/TextOutput.svelte";
  import TextInput from "./lib/components/TextInput.svelte";

  import {jValue, value} from "./lib/stores/valueStore.js";

  const convert = async () => {

    let data;
    const unsubscribe = value.subscribe((val) => data = val);

    const {result, valid, message} = await convertFromToml(data);

    if (valid) jValue.set(JSON.parse(result));
    else jValue.set(message);

    unsubscribe();

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

      <TextInput on:converted={convert}/>
      <TextOutput on:convert={convert} content={$jValue}/>

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

  p {
    margin: 0;
    line-height: 1.1;
  }

</style>
