<script>

    import { createEventDispatcher } from 'svelte';

    import {jsonHighlight} from "./scripts/json_prettify.js";

    export let content;

    $: jsonHighlighted = jsonHighlight(JSON.stringify(content, null, 4));
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

    }

</script>

{@html jsonStyle}

<div class="field">

    <div class="controls">

        <button on:click={convertDispatch} class="top">Convert</button>
        <button on:click={copyToClipboard} class="top">Copy to Clipboard</button>
        <button class="top">Settings</button>

    </div>

    <pre class="textarea" id="out">
{@html jsonHighlighted}
    </pre>

</div>


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
        justify-content: space-evenly;
        padding-bottom: 2px;
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
        overflow: scroll;
        margin-top: 0;
        margin-bottom: 0;
    }

</style>