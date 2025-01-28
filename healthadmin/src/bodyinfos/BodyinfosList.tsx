import { Datagrid, DateField, List, TextField, ReferenceField } from 'react-admin';

export const BodyinfoList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <ReferenceField source="user" reference="users"  link="show"/>
            <DateField source="measuretime" />
            <TextField source="height" />
            <TextField source="weight" />
            <TextField source="waist" />
        </Datagrid>
    </List>
);

export default BodyinfoList;