import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const CommonriskscaleList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="sex" />
            <NumberField source="age" />
            <TextField source="avgrisk" />
            <TextField source="minrisk" />
        </Datagrid>
    </List>
);

export default CommonriskscaleList;