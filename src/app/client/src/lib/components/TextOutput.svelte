<script>

    import { createEventDispatcher } from 'svelte';

    import toast, {Toaster} from "svelte-french-toast";

    import {jsonHighlight} from "../scripts/json_prettify.js";
    import DropdownModal from "./DropdownModal.svelte";


    let settingsOpen = false;
    let indentationSpacing = 4;
    export let content;

    $: jsonHighlighted = jsonHighlight(JSON.stringify(content, null, indentationSpacing));
    $: jsonStyle = `<style>
                    .string { color: #E69F66; }
                    .number { color: #B5CEA8; }
                    .boolean { color: #7FB5E1; }
                    .null { color: #D4D4D4; }
                    .key { color: #CDA869; }
                    </style>`;

    const dispatch = createEventDispatcher();

    const convertDispatch = () => {
        dispatch('convert', {});
    };

    const copyToClipboard = () => {

        const clipContent = (element) => {

          const range = document.createRange();
          range.selectNodeContents(element);

          const sel = window.getSelection();
          sel.removeAllRanges();
          sel.addRange(range);

          navigator.clipboard.writeText(sel.toString());

          sel.removeAllRanges();
        };

        clipContent(document.getElementById('out'));

        toast.success('Copied to clipboard!', {
            position: "bottom-center",
            style: "border: 1px solid #242424; padding: 16px; color: #242424;",
            iconTheme: {
                primary: '#535bf2',
                secondary: '#FFFAEE'
            }
        });
    }

    const handleSettings = (event) => {

        const button = document.querySelector('.dropdown-container');
        if (event.target === button && button.contains(event.target)) {
            settingsOpen = !settingsOpen;
        }
    }

    const changeIndentation = (event) => {

        let newIndent = event.detail.value;

        if (newIndent === "TAB") indentationSpacing = "\t";
        else indentationSpacing = parseInt(newIndent, 10);

    }

</script>

{@html jsonStyle}

<div class="field">

    <div class="controls">

        <button on:click={convertDispatch} class="top">Convert</button>
        <button on:click={copyToClipboard} class="top">Copy to Clipboard</button>

        <button on:click={(event) => handleSettings(event)} class="dropdown-container">Settings

            {#if settingsOpen}
                <DropdownModal on:indentation={changeIndentation}/>
            {/if}

        </button>

    </div>

    <pre class="textarea" id="out">
{@html jsonHighlighted}
    </pre>

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

    .dropdown-container {
        flex: 1;
        display: inline-block;
        position: relative;
        margin: 3px;
    }

    .top {
        flex: 1;
        margin: 3px;
    }

    .textarea {
        padding-top: 30px;
        padding-left: 10px;
        padding-right: 10px;
        overflow-wrap: break-word;
        text-align: left;
    }

    pre {
        font-size: 18px;
        width: 882px;
        height: 700px;
        overflow: auto;
        margin-top: 0;
        margin-bottom: 0;
    }


</style>