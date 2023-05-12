<script>

    import { createEventDispatcher } from 'svelte';

    let rangeList = ["4", "TAB", "1", "2", "3"];
    let currentIndent = 0;

    const dispatch = createEventDispatcher();

    const indentDispatch = () => {
        dispatch('indentation', {value: rangeList[currentIndent]});
    };

    const next = () => {
        if (currentIndent === 4) currentIndent = 0;
        else currentIndent++;
        indentDispatch();
    };


    const prev = () => {
        if (currentIndent === 0) currentIndent = 4;
        else currentIndent--;
        indentDispatch();
    };

</script>

<div class="dropdown" id="dp">

    <div class="indentation">


        <div class="control-indentation">

            <p>Indent Spacing</p>
            <button on:click={prev}>-</button>
            <p><strong>{rangeList[currentIndent]}</strong></p>
            <button on:click={next}>+</button>

        </div>

    </div>

</div>

<style>


    .dropdown {
        position: absolute;
        width: 100%;
        top: 100%;
        left: 0;
        z-index: 1;
        padding: 8px 0;
        margin-top: 4px;
        background: #242424;
        border-radius: 8px;
        border: 1px solid transparent;
        transition: border-color 0.25s;
        box-shadow: rgba(100, 108, 255, 0.2) 0px 8px 24px;
    }

    .dropdown:hover {
        border-color: #646cff;
    }


    .control-indentation {
        justify-content: center;
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .control-indentation > button {
        font-size: 20px;
        margin-left: 10px;
        margin-right: 10px;
    }

    .control-indentation > p {
        margin-left: 10px;
        padding-right: 10px;
    }

</style>