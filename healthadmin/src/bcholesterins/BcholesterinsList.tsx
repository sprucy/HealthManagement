import { Datagrid, DateField, List, NumberField, TextField, ReferenceField } from 'react-admin';

export const BcholesterinList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField source="user" reference="users"  link="show"/>
            <DateField source="measuretime" />
            <TextField source="TC" />
            <TextField source="LDL" />
            <TextField source="HDL" />
            <TextField source="TG" />
        </Datagrid>
    </List>
);

export default BcholesterinList;