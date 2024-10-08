var unitsData=[{"code":"ICT10001", "desc":"1 Problem Solving with ICT" },
{"code":"COS10005", "desc":"2 Web Development" },
{"code":"INF10003", "desc":"3 Introduction to Business Information Systems" },
{"code":"INF10002", "desc":"4 Database Analysis and Design" },
{"code":"COS10009", "desc":"5 Introduction to Programming" },
{"code":"INF30029", "desc":"6 Information Technology Project Management" },
{"code":"ICT30005", "desc":"7 Professional Issues in Information Technology" },
{"code":"ICT30001", "desc":"8 Information Technology Project" },
{"code":"COS20001", "desc":"9 User-Centred Design" },
{"code":"TNE10005", "desc":"10 Network Administration" },
{"code":"COS20016", "desc":"11 Operating System Configuration" },
{"code":"SWE20001", "desc":"12 Development Project 1 - Tools and Practices"},
{"code":"COS20007", "desc":"13 Object Oriented Programming"},
{"code":"COS30015", "desc":"14 IT Security"},
{"code":"COS30043", "desc":"15 Interface Design and Development"},
{"code":"COS30017", "desc":"16 Software Development for Mobile Devices" },
{"code":"INF20012", "desc":"17 Enterprise Systems" },
{"code":"ACC10007", "desc":"18 Financial Information for Decision Making" },
{"code":"INF20003", "desc":"19 Requirements Analysis and Modelling" },
{"code":"ACC20014", "desc":"20 Management Decision Making" },
{"code":"INF30005", "desc":"21 Business Process Management" },
{"code":"INF30003", "desc":"22 Business Information Systems Analysis" },
{"code":"INF30020", "desc":"23 Information Systems Risk and Security" },
{"code":"INF30001", "desc":"24 Systems Acquisition & Implementation Management" }]

const StudentMarks = {
    components: {
        paginate: VuejsPaginateNext,
    },

    data: function () {
        return {
            currentPage: 1,
            units: unitsData,
            editUnitIndex: null,
            editedUnit: { code: '', desc: '' }
        }
    },

    template: `
    <div>
        <h1>Unit Descriptions</h1>

        <v-table class="table table-striped" border="1">
            <thead>
                <tr>
                    <th scope="col" id="code">Code</th>
                    <th scope="col" id="desc">Description</th>
                    <th scope="col">Actions</th> <!-- New column for actions -->
                </tr>
            </thead>

            <tbody>
                <tr v-for="(unit, index) in getItems">
                    <td :headers="['code']">{{unit.code}}</td>
                    <td :headers="['desc']">{{unit.desc}}</td>
                    <td>
                        <button @click="editUnit(unit, index)" class="btn btn-sm btn-primary">Edit</button>
                        <button @click="deleteUnit(unit, index)" class="btn btn-sm btn-danger">Delete</button>
                    </td>
                </tr>
            </tbody>
        </v-table>

        <!-- Inputs for new unit -->
        <div class="mt-3">
            <label for="newUnitCode">Code:</label>
            <input type="text" id="newUnitCode" v-model="newUnitcode" class="form-control mb-2">
            <label for="newUnitDesc">Description:</label>
            <input type="text" id="newUnitDesc" v-model="newUnitdesc" class="form-control mb-2">
            <button @click="insertUnit" class="btn btn-primary">Insert</button>
        </div>

        <!-- Vue Paginate template -->
        <paginate 
            :page-count="14"    
            :page-range="5" 
            :margin-pages="1"
            :click-handler="clickCallback" 
            :prev-text=" 'Prev Page' " 		
            :next-text="'Next Page'" 
            :container-class="'pagination'" 
            :active-class="'currentPage'"
        >
        </paginate>
    </div>
    `,

    computed: {
        getItems: function () {
            let current = this.currentPage * 2;
            let start = current - 2;
            return this.units.slice(start, current);
        }
    },
    methods: {
        clickCallback: function (pageNum) {
            this.currentPage = Number(pageNum);
        },
        editUnit(unit, index) {
            unit.code = this.newUnitcode;
            unit.desc = this.newUnitdesc;
            
            this.newUnitcode = '';
            this.newUnitdesc = '';
        },
        deleteUnit(unit, index) {
            this.units.splice(index, 1);
        },
        insertUnit() {
            this.units.push({ code: this.newUnitcode, desc: this.newUnitdesc });
            this.newUnitcode = '';
            this.newUnitdesc = '';
        }
    }
};