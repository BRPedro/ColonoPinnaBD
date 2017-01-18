create or replace function filtrarPatrones(limite float)
returns boolean as 
$BODY$
declare
	cursor_primario refcursor;
	cursor_secundario refcursor;
	
	id_p integer;
	x integer;
	y integer;
	contador_p integer;
	
	
	id_s integer;
	contador_s integer;
	
begin
	open cursor_primario for select idpatron,xp,yp,contadorp from paginas_tc_patron;
	loop
		fetch cursor_primario into id_p,x,y,contador_p;
		exit when not FOUND;
		open cursor_secundario for select idpatron,contadorp from paginas_tc_patron where idpatron<>id_p and @(|/(((x-paginas_tc_patron.xp)^2)+((y-paginas_tc_patron.yp)^2)))<=limite; 
		loop
		fetch cursor_secundario into id_s,contador_s;
		exit when not FOUND;
			if contador_p>contador_s then
				UPDATE paginas_tc_patron
				SET contadorp=contadorp+contador_s
				WHERE idpatron = id_p;

				delete from paginas_tc_patron where idpatron=id_s; 
			else
				UPDATE paginas_tc_patron
				SET contadorp=contadorp+contador_p
				WHERE idpatron = id_s;

				delete from paginas_tc_patron where idpatron=id_p; 
				
			end if;
		end loop;	
		close cursor_secundario;
		
	end loop;
	close cursor_primario;
	return true;
end;
$BODY$
language plpgsql;
