import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const BloodpressurescaleList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="sex" />
            <NumberField source="maxv" />
            <NumberField source="score" />
        </Datagrid>
    </List>
);

export default BloodpressurescaleList;