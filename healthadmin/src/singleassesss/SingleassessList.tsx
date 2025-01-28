import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const SingleassessList = () => (
    <List>
        <Datagrid>
            <TextField source="id" />
            <TextField source="assesstype" />
            <TextField source="assessname" />
            <NumberField source="minv" />
            <NumberField source="maxv" />
        </Datagrid>
    </List>
);

export default SingleassessList;