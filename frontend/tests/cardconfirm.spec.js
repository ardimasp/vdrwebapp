import { mount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import CardConfirm from '../src/views/cards/CardConfirm.vue'

describe("CardConfirm:", () => {
    let localVue, vuetify, wrapper;

    beforeEach(() => {
        localVue = createLocalVue();
        vuetify = new Vuetify();

        const elem = document.createElement('div')
        if (document.body) {
            document.body.appendChild(elem)
        }

        const App = localVue.component('App', {
            components: {CardConfirm},
            data() {
                return{
                    dialog: false,
                }
            },
            template: `
                <v-app>
                    <CardConfirm />
                </v-app>
            `
        });

        wrapper = mount(App, {
            localVue, 
            vuetify, 
            // attachToDocument:true,
            attachTo: elem,
        });
    })


    it('should open dialog', () => {
        const confirmButton = wrapper.find('[data-testid="dialog-confirm"]');

        expect(confirmButton.exists()).toBe(true);
        expect(wrapper.vm.$data.dialog).toBe(true);
    });

    it('should change dialog to false after click', async () => {
        const confirmButton = wrapper.find('[data-testid="dialog-confirm"]');
        confirmButton.vm.$emit('click');

        await wrapper.vm.$nextTick();
        expect(wrapper.vm.$data.dialog).toBe(false);
    })
})
