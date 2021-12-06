<template>
  <div class="home">
    <h1 v-ripple>Startseite</h1>
    <p>Willkommen zur interaktiven erklärbaren AI.</p>
    <p>Diese AI Applikation gibt Bewertungen zur Bewilligung von Bankkrediten auf der Basis von Wissen, was sie Trainingsdaten gelernt hat.</p>
    <p>Außerdem werden zu den Entscheidungen, die die AI trifft Erklärungen von verschiedenen Gesichtspunkten aus gegeben und dargestellt, mit deren Hilfe sich die Enzscheidung nachvollziehen lässt .</p>
    <router-link to="/level1"><q-btn color="primary" label="Get started"/></router-link>
  </div>
</template>

<script>

export default {
  name: 'Home', 
  components: { }
}
</script>

<style scoped>
  button {
     margin-top: 80px;
     border: none;
     background-color: blue;
     color: white;
     height: 60px;
     width: 140px;
     border-radius: 5%;
  }
</style>
