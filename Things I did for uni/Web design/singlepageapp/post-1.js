const Post = {
    data() {
        return {
            statPosts: [],
            strStatus: ''
        };
    },
    template: `
        <div>
            <div class="mb-3">
                <label for="status" class="form-label">Status:</label>
                <input type="text" id="status" v-model="strStatus" class="form-control" required>
            </div>
            <button @click="addStatus" class="btn btn-primary">Post</button>

            <div class="mt-3">
                <div v-for="(status, index) in statPosts" :key="index" class="alert alert-primary">
                    <p>{{ status }}</p>
                    <button @click="removeStatus(index)" class="btn btn-danger">Delete</button>
                </div>
            </div>
        </div>
    `,
    methods: {
        addStatus() {
            if (this.strStatus.trim() !== '') {
                this.statPosts.unshift(this.strStatus);
                this.strStatus = '';
            }
        },
        removeStatus(index) {
            this.statPosts.splice(index, 1);
        }
    }
};

Vue.component('Post', Post);