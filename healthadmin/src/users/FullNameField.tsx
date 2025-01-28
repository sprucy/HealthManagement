import * as React from 'react';
import { SxProps, Typography } from '@mui/material';
import { memo } from 'react';
import { FieldProps, useRecordContext } from 'react-admin';

import AvatarField from './AvatarField';

interface Props extends FieldProps {
    size?: string;
    sx?: SxProps;
}

const FullNameField = (props: Props) => {
    const { size } = props;
    const record = useRecordContext();
    return record ? (
        <Typography
            variant="body2"
            display="flex"
            flexWrap="nowrap"
            alignItems="center"
            component="div"
            sx={props.sx}
        >
            <AvatarField
                record={record}
                size={size}
                sx={{
                    mr: 1,
                    mt: -0.5,
                    mb: -0.5,
                }}
            />
            {record.last_name} {record.first_name} 
        </Typography>
    ) : null;
};

export default memo<Props>(FullNameField);
