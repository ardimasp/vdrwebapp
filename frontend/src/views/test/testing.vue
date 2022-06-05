<template>
    <div>
        <v-btn @click="checkList" color="primary">AAAAAAAAAAAA</v-btn>
        {{list}}
    </div>
</template>

<script>
import { defineComponent, ref } from '@vue/composition-api'
import store from '../../store'

export default defineComponent({
    setup() {
        const list = store.state.tree.list;

        const checkList = () => {
            for (let i = 0; i < list.length; i++){
                console.log("looping", i, "...");
                searchList(list[i]);

                if(search.value) break;
                continue;
            }

            search.value = false;
            console.log("..........................................")
        }

        const search = ref(false);
        const searchList = (item) => {
            search.value = false;
            if(item.type == "folder") {
                console.log("inside folder", item.children);
                if(item.children.length){
                    console.log("this folder is not empty!");
                    if(item.children.find(x => x.id == 5)){
                        console.log("file is found...");
                        search.value = true;
                    }
                    else searchList(item.children);
                } else console.log("folder is empty");
            }
            else if (item.length){
                console.log("relooping...");
                reSearchList(item);
            }
            return
        }

        const reSearchList = (item) => {
            for(let i = 0; i < item.length; i++){
                console.log("the inside of item", item[i])
                searchList(item[i])

                if(search.value) break;
                continue;
            }
        }

        return {list, checkList};
    },
})
</script>
