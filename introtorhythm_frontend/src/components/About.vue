<template>
    <div id="info">
        <div id="info-wrapper">
            <div v-html="info"></div>

            <br>
            <br>
            <div id="arrow">
                &#8681;
            </div>
            <div>
                <form action="https://www.paypal.com/donate" method="post" target="_blank">
                    <input type="hidden" name="hosted_button_id" value="WUK6JYHURH6KJ" />
                    <input id="donate" type="submit" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" value="DONATE TO I2R">
                    <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { useContentStore } from '@/stores';

const contentStore = useContentStore();

const info = computed(() => {
    return contentStore.about?.info;
});
</script>
