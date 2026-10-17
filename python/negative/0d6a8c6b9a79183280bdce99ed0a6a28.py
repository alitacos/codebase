def get_info_of_chemical_elements_in_periodic_table_elements_dict_list(elements=[], all_=True, name=False, appearance=False, atomic_mass=False, boil=False, category=False, density=False, discovered_by=False, melt=False, molar_heat=False, named_by=False, number=False, period=False, group=False, phase=False, source=False, bohr_model_image=False, bohr_model_3d=False, spectral_img=False, summary=False, symbol=False, xpos=False, ypos=False, wxpos=False, wypos=False, shells=False, electron_configuration=False, electron_configuration_semantic=False, electron_affinity=False, electronegativity_pauling=False, ionization_energies=False, cpk_hex=False, image=False, block=False):
    """Returns filtered chemical element data based on requested properties.

    Args:
        all_: If True, returns all properties (default)
        [property]_: Set to True to include specific property in results
    """
    if all_:
        return elements
    else:
        requested_props = []
        args = locals()
        for prop, requested in args.items():
            if prop not in ['all_', 'elements'] and requested:
                requested_props.append(prop)
        filtered_data = []
        for element in elements:
            filtered_element = {}
            for prop in requested_props:
                json_prop = prop.replace('_', '-') if prop in ['cpk_hex'] else prop
                if json_prop in element:
                    filtered_element[prop] = element[json_prop]
            filtered_data.append(filtered_element)
        return filtered_data