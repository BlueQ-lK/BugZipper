<template>
    <div class="coming">
        <img src="../assets/bg-img.jpg" alt="">
        <h1>
            Coming Soon.
        </h1>
    </div>
</template>

<style scoped>
.coming {
    width: 100%;
    height: calc(100vh - 5.5rem);
    overflow: hidden;
    margin: 1rem 0;
    border-radius: 20px;
    position: relative;
    user-select: none;
}

img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    opacity: 0.4;
    z-index: -1111;
}

h1 {
    font-size: 90px;
    position: absolute;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
}
</style>