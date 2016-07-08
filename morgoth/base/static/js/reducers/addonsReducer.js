import {
  FETCH_ADDONS, FETCH_ADDONS_SUCCESS, FETCH_ADDONS_FAILURE, RESET_ADDONS
} from '../actions/addons';


const INITIAL_STATE = {
  addonsList: {
    addons: [],
    error: null,
    loading: false
  }
};

export default (state=INITIAL_STATE, action) => {
  let error;

  switch (action.type) {
    case FETCH_ADDONS:
      return {
        ...state,
        addonsList: {
          addons: [],
          error: null,
          loading: true
        }
      };

    case FETCH_ADDONS_SUCCESS:
      return {
        ...state,
        addonsList: {
          addons: action.payload.data,
          error: null,
          loading: false
        }
      };

    case FETCH_ADDONS_FAILURE:
      error = action.payload.data || {message: action.payload.message};
      return {
        ...state,
        addonsList: {
          addons: [],
          error: error,
          loading: false
        }
      };

    case RESET_ADDONS:
      return {
        ...state,
        addonsList: {
          addons: [],
          error: null,
          loading: false
        }
      };

    default:
      return state;
  }
};
