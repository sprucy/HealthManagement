import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const RiskevaluatscaleList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="sex" />
            <NumberField source="score" />
            <TextField source="risk" />
        </Datagrid>
    </List>
);
export default RiskevaluatscaleList;