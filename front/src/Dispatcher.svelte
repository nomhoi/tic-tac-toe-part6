<script>
    import { history, status } from './stores.js';
    import { Command } from './helpers.js';

	let promise = null;
	let promise_number = null;

	async function getResult(task_id) {
		var i = 1;
		var timerId = setTimeout(async function go() {
			console.log("Result request: " + i);
			console.log("Task Id: " + task_id)
			const res = await fetch(`result/` + task_id);
			const response = await res.text();

			if (res.ok) {
				let result = JSON.parse(response);
				console.log(result)

				if (result.state === 'SUCCESS') {
					let i = parseInt(result.number);

					if ($status === 1 || $history.state.squares[i]) {
						promise_number = result.number + ' - busy';
						return;
					}

					promise_number = i;
					history.push(new Command($history.state, i));
					return;
				}
			}

			if (i < 5) 
				setTimeout(go, 500);
			i++;
		}, 500);
	}	

	async function getRandomNumber() {
		const res = await fetch(`number`);
		const text = await res.text();

		if (res.ok) {
			await getResult(text);
			return text;
		} else {
			throw new Error(text);
		}
	}

	function handleClick() {
		promise_number = null;
		promise = getRandomNumber();
	}

	//setInterval(handleClick, 500);
</script>

{#if $status > 0}
    <button disabled>
        Get random number
    </button>
{:else}
    <button on:click={handleClick}>
        Get random number
    </button>
{/if}

{#await promise}
	<p>...подождите</p>
{:then taskid}
	<p>Task Id: {taskid}</p>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}


{#await promise_number}
	<p>...подождите</p>
{:then number}
	<p>Number: {number}</p>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}