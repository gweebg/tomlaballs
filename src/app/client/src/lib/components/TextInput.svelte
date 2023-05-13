<script>

  import toast, {Toaster} from "svelte-french-toast";

  import {shortcut} from "../scripts/shortcut.js";

  import { createEventDispatcher } from 'svelte';
  import {value} from "../stores/valueStore.js";

  let tomlValue = "";
  let files;

  const dispatch = createEventDispatcher();

  const dispachChange = () => {
      dispatch('converted');
  };

  const updateValue = () => {
      value.set(tomlValue);
  }

  const handleUpload = async () => {

      let content = await files[0].text();
      value.set(content);
      tomlValue = content;

      toast.success('File Loaded!', {
            position: "bottom-center",
            style: "border: 1px solid #242424; padding: 16px; color: #242424;",
            iconTheme: {
                primary: '#535bf2',
                secondary: '#FFFAEE'
            }
        });

  }

</script>

<div class="field">

    <div class="controls">
        <label for="inputFile" class="file-input">
            Upload File
            <input id="inputFile" bind:files on:change={handleUpload} type="file">
        </label>
    </div>

    <div class="input-field">

        <textarea
            name="toml_value"
            id="toml" cols="70"
            rows="27"
            placeholder="Insert your TOML code here."
            bind:value={tomlValue}
            on:input={updateValue}
            use:shortcut={{control: true, code: 'Enter', callback: () => dispachChange()}}></textarea>

    </div>

</div>

<Toaster/>

<style>

    .field {
        padding: 10px;
        margin-left: 20px;
        transition: border-color 0.25s;
        width: 892px;
        height: 774px;
        background: #2B2A33;
        border: solid 1px #2B2A33;
        border-radius: 5px;
    }

    .field:hover {
        border-color: #646cff;
    }

    .field:focus {
        outline: none #646cff;
    }

    .controls {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        padding-bottom: 2px;
    }

    input[type="file"] {
        display: none;
    }

    .file-input {

        flex: 1;
        margin: 3px;
        border-radius: 8px;
        border: 1px solid transparent;
        padding: 0.6em 1.2em 1.2em 5.2px;
        font-size: 1em;
        font-weight: 500;
        font-family: inherit;
        background-color: #242424;
        cursor: pointer;
        transition: border-color 0.25s;
        text-align: center;
    }

    .file-input:hover {
        border-color: #646cff;
    }

    .file-input:focus,
    .file-input:focus-visible {
      outline: 4px auto -webkit-focus-ring-color;
    }

    textarea {
        resize: none;
        font-size: 18px;
        padding: 30px 10px 10px;
        border: none;
        background-color: inherit;
    }

    textarea:focus {
        outline: none;
    }

</style>