import { BooleanField, Datagrid, List, NumberField, TextField } from 'react-admin';

export const DiabetesscaleList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="sex" />
            <BooleanField source="diabetes" />
            <NumberField source="score" />
        </Datagrid>
    </List>
);

export default DiabetesscaleList;