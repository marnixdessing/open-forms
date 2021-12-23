import React from 'react';
import PropTypes from 'prop-types';
import {FormattedMessage, useIntl} from 'react-intl';

import {Checkbox, TextInput} from '../../../forms/Inputs';
import ComponentSelection from '../../../forms/ComponentSelection';
import {ChangelistTableWrapper, HeadColumn, TableRow} from '../../../tables';


const HeadColumns = () => {
    const intl = useIntl();

    const enabledText = (<FormattedMessage
        description="Manage process vars enabled checkbox column title"
        defaultMessage="Enabled"
    />);
    const enabledHelp = intl.formatMessage({
        description: 'Manage process vars enabled checkbox help text',
        defaultMessage: 'Check to include the field as process variable',
    });

    const componentText = (<FormattedMessage
        description="Manage process vars component column title"
        defaultMessage="Field"
    />);
    const componentHelp = intl.formatMessage({
        description: 'Manage process vars component help text',
        defaultMessage: 'The value of the selected field will be the process variable value.',
    });

    const aliasText = (<FormattedMessage
        description="Manage process vars alias column title"
        defaultMessage="Alias"
    />);
    const aliasHelp = intl.formatMessage({
        description: 'Manage process vars alias help text',
        defaultMessage: 'If desired, you can specify a different process variable name.',
    });

    return (
        <>
            <HeadColumn content={enabledText} title={enabledHelp} />
            <HeadColumn content={componentText} title={componentHelp} />
            <HeadColumn content={aliasText} title={aliasHelp} />
        </>
    );
};


const ProcessVariable = ({ index, enabled=true, componentKey='', alias='', onChange }) => {
    const onCheckboxChange = (event, current) => {
        const { target: {name} } = event;
        onChange({target: {name, value: !current}});
    };

    return (
        <TableRow index={index}>
            <Checkbox
                name="enabled"
                label=""
                checked={enabled}
                onChange={event => onCheckboxChange(event, enabled)}
            />
            {/* TODO: add filter prop to only show unmapped components */}
            <ComponentSelection name="componentKey" value={componentKey} onChange={onChange} />
            <TextInput name="alias" value={alias} onChange={onChange} placeholder={componentKey} />
        </TableRow>
    );
};

ProcessVariable.propTypes = {
    index: PropTypes.number.isRequired,
    enabled: PropTypes.bool,
    componentKey: PropTypes.string,
    alias: PropTypes.string,
    onChange: PropTypes.func.isRequired,
};


const SelectProcessVariables = ({ processVariables=[], onChange }) => {
    return (
        <ChangelistTableWrapper headColumns={<HeadColumns />}>
            {
                processVariables.map((processVar, index) => (
                    <ProcessVariable key={index} index={index} onChange={onChange.bind(null, index)} {...processVar} />
                ))
            }
        </ChangelistTableWrapper>
    );
};

SelectProcessVariables.propTypes = {
    processVariables: PropTypes.arrayOf(PropTypes.shape({
        enabled: PropTypes.bool,
        componentKey: PropTypes.string,
        alias: PropTypes.string,
    })),
    onChange: PropTypes.func.isRequired,
    // onAdd: PropTypes.func.isRequired,
    // onDelete: PropTypes.func.isRequired,
};


export default SelectProcessVariables;
