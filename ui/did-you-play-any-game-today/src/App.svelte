<script lang="ts">
  import "animate.css";
  import confetti from "canvas-confetti";

  let disabled = false;
  let submitted = false;

  function animate() {
    const end = Date.now() + 15 * 1000;

    // go Buckeyes!
    const colors = ["#bb0000", "#ffffff"];

    (function frame() {
      confetti({
        particleCount: 2,
        angle: 60,
        spread: 55,
        origin: { x: 0 },
        colors: colors,
      });
      confetti({
        particleCount: 2,
        angle: 120,
        spread: 55,
        origin: { x: 1 },
        colors: colors,
      });

      if (Date.now() < end) {
        requestAnimationFrame(frame);
      } else {
        disabled = false;
      }
    })();
  }

  async function click() {
    try {
      submitted = false;
      disabled = true;
      const resp = await fetch("api/game/play", {
        method: "POST",
        body: "",
      });
      if (!resp.ok) {
        throw new Error(`invalid response: ${resp.status} ${resp.statusText}`);
      }
      console.debug(`api response: ${await resp.text()}`);
      animate();
      submitted = true;
    } catch (ex) {
      console.error(ex);
    }
  }
</script>

<main>
  <h2>Did You Play Any Game Today?</h2>
  <button
    class="button animate__repeat-2"
    class:animate__animated={submitted}
    class:animate__tada={submitted}
    on:click={click}
    {disabled}
  >
    <span> 🎉 </span>
    <span>Yes!</span>
  </button>
</main>

<style>
  main {
    display: flex;
    align-items: center;
    flex-direction: column;
  }
  button {
    cursor: pointer;
    font: inherit;
    margin: 5rem 0;
    padding: 0;
  }

  .button {
    background-color: #404663;
    color: #fff;
    border: 0;
    font-size: 2rem;
    font-weight: 400;
    padding: 0.5em 1.25em;
    border-radius: 0.5em;
    z-index: 999;
    position: relative;
    display: flex;
    gap: 0.5em;
    box-shadow: 0px 1.7px 2.2px rgba(0, 0, 0, 0.02),
      0px 4px 5.3px rgba(0, 0, 0, 0.028), 0px 7.5px 10px rgba(0, 0, 0, 0.035),
      0px 13.4px 17.9px rgba(0, 0, 0, 0.042),
      0px 25.1px 33.4px rgba(0, 0, 0, 0.05), 0px 60px 80px rgba(0, 0, 0, 0.07);
  }

  .button:active {
    transform: scale(1.01);
  }
</style>
