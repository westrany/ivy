# global
import numpy as np
from hypothesis import assume, given, strategies as st

# local
import ivy
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


# flip
@handle_cmd_line_args
@given(
    dtype_and_values=helpers.dtype_and_values(
        shape=st.shared(helpers.get_shape(min_num_dims=1), key="shape"),
        available_dtypes=helpers.get_dtypes("float"),
    ),
    axis=helpers.get_axis(
        shape=st.shared(helpers.get_shape(min_num_dims=1), key="shape"),
        force_tuple=True,
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.flip"
    ),
)
def test_torch_flip(
    dtype_and_values,
    axis,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, value = dtype_and_values
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="flip",
        input=np.asarray(value, dtype=input_dtype),
        dims=axis,
    )


# roll
@handle_cmd_line_args
@given(
    dtype_and_values=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        shape=st.shared(helpers.get_shape(min_num_dims=1), key="shape"),
    ),
    shift=helpers.get_axis(
        shape=st.shared(helpers.get_shape(min_num_dims=1), key="shape"),
    ),
    axis=helpers.get_axis(
        shape=st.shared(helpers.get_shape(min_num_dims=1), key="shape"),
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.roll"
    ),
)
def test_torch_roll(
    dtype_and_values,
    shift,
    axis,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, value = dtype_and_values
    if isinstance(shift, int) and isinstance(axis, tuple):
        axis = axis[0]
    if isinstance(shift, tuple) and isinstance(axis, tuple):
        if len(shift) != len(axis):
            mn = min(len(shift), len(axis))
            shift = shift[:mn]
            axis = axis[:mn]
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="roll",
        input=np.asarray(value, dtype=input_dtype),
        shifts=shift,
        dims=axis,
    )


# fliplr
@handle_cmd_line_args
@given(
    dtype_and_values=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        shape=helpers.get_shape(min_num_dims=2),
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.fliplr"
    ),
)
def test_torch_fliplr(
    dtype_and_values,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, value = dtype_and_values
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="fliplr",
        input=np.asarray(value, dtype=input_dtype),
    )


# cumsum
@handle_cmd_line_args
@given(
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        max_num_dims=5,
        valid_axis=True,
        allow_neg_axes=False,
        max_axes_size=1,
        force_int_axis=True,
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.cumsum"
    ),
    dtype=helpers.get_dtypes("numeric", none=True),
)
def test_torch_cumsum(
    dtype_x_axis,
    as_variable,
    num_positional_args,
    native_array,
    with_out,
    dtype,
    fw,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="cumsum",
        input=np.asarray(x, dtype=input_dtype),
        dim=axis,
        dtype=dtype,
        out=None,
    )


@st.composite
def dims_and_offset(draw, shape):
    shape_actual = draw(shape)
    dim1 = draw(helpers.get_axis(shape=shape, force_int=True))
    dim2 = draw(helpers.get_axis(shape=shape, force_int=True))
    offset = draw(
        st.integers(min_value=-shape_actual[dim1], max_value=shape_actual[dim1])
    )
    return dim1, dim2, offset


@handle_cmd_line_args
@given(
    dtype_and_values=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        shape=st.shared(helpers.get_shape(min_num_dims=2), key="shape"),
    ),
    dims_and_offset=dims_and_offset(
        shape=st.shared(helpers.get_shape(min_num_dims=2), key="shape")
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.diagonal"
    ),
)
def test_torch_diagonal(
    dtype_and_values,
    dims_and_offset,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, value = dtype_and_values
    dim1, dim2, offset = dims_and_offset
    input = np.asarray(value, dtype=input_dtype)
    num_dims = len(np.shape(input))
    assume(dim1 != dim2)
    if dim1 < 0:
        assume(dim1 + num_dims != dim2)
    if dim2 < 0:
        assume(dim1 != dim2 + num_dims)
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="diagonal",
        input=input,
        offset=offset,
        dim1=dim1,
        dim2=dim2,
    )


@handle_cmd_line_args
@given(
    dtype_and_values=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        min_num_dims=2,  # Torch requires this.
    ),
    diagonal=st.integers(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.triu"
    ),
)
def test_torch_triu(
    dtype_and_values,
    diagonal,
    fw,
    num_positional_args,
    as_variable,
    with_out,
    native_array,
):
    dtype, values = dtype_and_values
    values = np.asarray(values, dtype=dtype)
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="triu",
        input=values,
        diagonal=diagonal,
    )


# cumprod
@handle_cmd_line_args
@given(
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        max_num_dims=5,
        valid_axis=True,
        allow_neg_axes=False,
        max_axes_size=1,
        force_int_axis=True,
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.cumprod"
    ),
    dtype=helpers.get_dtypes("numeric", none=True),
)
def test_torch_cumprod(
    dtype_x_axis,
    as_variable,
    num_positional_args,
    native_array,
    with_out,
    dtype,
    fw,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="cumprod",
        input=np.asarray(x, dtype=input_dtype),
        dim=axis,
        dtype=dtype,
        out=None,
    )


@handle_cmd_line_args
@given(
    row=st.integers(min_value=0, max_value=10),
    col=st.integers(min_value=0, max_value=10),
    offset=st.integers(),
    dtype_result=helpers.get_dtypes("valid"),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.tril_indices"
    ),
)
def test_torch_tril_indices(
    row,
    col,
    offset,
    dtype_result,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    fw,
):
    helpers.test_frontend_function(
        input_dtypes=[ivy.int32],
        with_out=with_out,
        num_positional_args=num_positional_args,
        as_variable_flags=as_variable,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="tril_indices",
        row=row,
        col=col,
        offset=offset,
        dtype=dtype_result,
    )
