const NameTest = {
    data() {
        return {
            strName: '',
            submitted: false
        };
    },
    template: `
        <h1>String Test</h1>
        <div class="row">
            <div class="col-sm-6">
                <p>
                    <label for="nameInput">Please enter your name:</label>
                    <input type="text" id="nameInput" v-model="strName" class="form-control" />
                </p>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-6">
                <button @click="checkName" class="btn btn-primary">Submit</button>
                <p v-show="submitted && strName.toLowerCase() === 'mark'">Awesome name!</p>
                <p v-show="submitted && strName.toLowerCase() !== 'mark'">{{ strName }} is not my name</p>
            </div>
        </div>
    `,
    watch: {
        strName() {
            this.submitted = false;
        }
    },
    methods: {
        checkName() {
            this.submitted = true;
        }
    }
};

Vue.component('NameTest', NameTest);