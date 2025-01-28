import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const TCscaleList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="sex" />
            <TextField source="maxv" />
            <NumberField source="score" />
        </Datagrid>
    </List>
);

export default TCscaleList;